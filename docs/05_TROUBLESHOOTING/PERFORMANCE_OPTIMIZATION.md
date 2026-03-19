# Performance Optimization Guide

## Overview

This guide provides comprehensive strategies for optimizing the SOC Job Task Analyzer pipeline performance, covering memory management, computational efficiency, I/O operations, and parallel processing techniques.

## Memory Optimization

### Memory Profiling and Analysis

**Memory Usage Monitoring**:
```python
import psutil
import os
from contextlib import contextmanager

class MemoryProfiler:
    """Monitor memory usage throughout pipeline execution"""

    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.snapshots = []

    def take_snapshot(self, label=""):
        """Take a memory usage snapshot"""

        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()

        snapshot = {
            'timestamp': time.time(),
            'label': label,
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'memory_percent': memory_percent,
            'cpu_percent': self.process.cpu_percent()
        }

        self.snapshots.append(snapshot)
        return snapshot

    def get_memory_report(self):
        """Generate memory usage report"""

        if not self.snapshots:
            return {}

        rss_values = [s['rss_mb'] for s in self.snapshots]
        memory_percents = [s['memory_percent'] for s in self.snapshots]

        return {
            'peak_memory_mb': max(rss_values),
            'average_memory_mb': sum(rss_values) / len(rss_values),
            'memory_increase_mb': rss_values[-1] - rss_values[0] if len(rss_values) > 1 else 0,
            'peak_memory_percent': max(memory_percents),
            'snapshots': self.snapshots
        }

@contextmanager
def memory_monitor(stage_name):
    """Context manager for monitoring memory usage of code blocks"""

    profiler = MemoryProfiler()
    initial_snapshot = profiler.take_snapshot(f"{stage_name}_start")

    logger = logging.getLogger('performance.memory')
    logger.info(f"Starting memory monitoring for {stage_name}: {initial_snapshot['rss_mb']:.1f} MB")

    try:
        yield profiler
    finally:
        final_snapshot = profiler.take_snapshot(f"{stage_name}_end")
        report = profiler.get_memory_report()

        logger.info(f"Memory monitoring completed for {stage_name}:")
        logger.info(f"  Peak memory: {report['peak_memory_mb']:.1f} MB")
        logger.info(f"  Memory increase: {report['memory_increase_mb']:+.1f} MB")
        logger.info(f"  Final memory: {final_snapshot['rss_mb']:.1f} MB")

        # Save memory report
        debug_collector.save_intermediate_state('performance', f'{stage_name}_memory', report)
```

### Data Structure Optimization

**Memory-Efficient Data Structures**:
```python
import sys
from typing import List, Dict, Any
import numpy as np

class MemoryEfficientTaskStorage:
    """Memory-efficient storage for task data"""

    def __init__(self):
        self.task_texts: List[str] = []
        self.task_metadata: List[Dict[str, Any]] = []
        self.text_to_index: Dict[str, int] = {}  # For deduplication

    def add_task(self, task_text: str, metadata: Dict[str, Any] = None):
        """Add task with deduplication"""

        # Check for exact duplicates
        if task_text in self.text_to_index:
            # Update metadata if needed
            existing_idx = self.text_to_index[task_text]
            if metadata:
                self.task_metadata[existing_idx].update(metadata)
            return existing_idx

        # Add new task
        idx = len(self.task_texts)
        self.task_texts.append(task_text)
        self.task_metadata.append(metadata or {})
        self.text_to_index[task_text] = idx

        return idx

    def get_task(self, index: int) -> Dict[str, Any]:
        """Retrieve task by index"""

        return {
            'text': self.task_texts[index],
            'metadata': self.task_metadata[index]
        }

    def get_memory_usage(self) -> Dict[str, float]:
        """Calculate memory usage of stored data"""

        text_memory = sum(sys.getsizeof(text) for text in self.task_texts)
        metadata_memory = sum(sys.getsizeof(meta) for meta in self.task_metadata)
        index_memory = sys.getsizeof(self.text_to_index)

        for key, value in self.text_to_index.items():
            index_memory += sys.getsizeof(key) + sys.getsizeof(value)

        total_memory = text_memory + metadata_memory + index_memory

        return {
            'total_mb': total_memory / 1024 / 1024,
            'text_mb': text_memory / 1024 / 1024,
            'metadata_mb': metadata_memory / 1024 / 1024,
            'index_mb': index_memory / 1024 / 1024,
            'task_count': len(self.task_texts)
        }

def optimize_task_data_loading(jobs_data):
    """Load and optimize task data for memory efficiency"""

    logger = logging.getLogger('performance.memory')

    # Initial memory usage
    initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    # Extract tasks efficiently
    task_storage = MemoryEfficientTaskStorage()

    for job in jobs_data:
        responsibilities = extract_responsibilities(job.get('description', ''))

        for resp in responsibilities:
            task_storage.add_task(resp, {
                'job_id': job.get('id'),
                'job_title': job.get('title'),
                'company': job.get('company_name'),
                'source': 'responsibilities'
            })

    # Memory usage after loading
    loaded_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    memory_increase = loaded_memory - initial_memory

    memory_report = task_storage.get_memory_usage()

    logger.info("Task data loading optimization:")
    logger.info(f"  Tasks loaded: {memory_report['task_count']}")
    logger.info(f"  Memory increase: {memory_increase:.1f} MB")
    logger.info(f"  Memory per task: {memory_report['total_mb'] / memory_report['task_count'] * 1024:.1f} KB")

    return task_storage
```

### Garbage Collection Optimization

**Proactive Memory Management**:
```python
import gc
import weakref

class MemoryManager:
    """Proactive memory management for long-running processes"""

    def __init__(self, memory_threshold_mb=1000, gc_interval_seconds=300):
        self.memory_threshold_mb = memory_threshold_mb
        self.gc_interval_seconds = gc_interval_seconds
        self.last_gc_time = time.time()
        self.gc_stats = []

    def check_memory_pressure(self):
        """Check if memory usage is above threshold"""

        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024

        return memory_mb > self.memory_threshold_mb

    def perform_garbage_collection(self, force=False):
        """Perform garbage collection if needed"""

        current_time = time.time()

        # Check if GC is due
        time_since_last_gc = current_time - self.last_gc_time
        should_gc = force or time_since_last_gc > self.gc_interval_seconds

        if should_gc and self.check_memory_pressure():
            logger = logging.getLogger('performance.memory')

            # Record memory before GC
            memory_before = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

            # Perform garbage collection
            collected = gc.collect()

            # Record memory after GC
            memory_after = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

            gc_stat = {
                'timestamp': current_time,
                'objects_collected': collected,
                'memory_before_mb': memory_before,
                'memory_after_mb': memory_after,
                'memory_freed_mb': memory_before - memory_after,
                'duration_seconds': time_since_last_gc
            }

            self.gc_stats.append(gc_stat)
            self.last_gc_time = current_time

            logger.info(f"Garbage collection performed: {collected} objects collected, "
                       f"{memory_before - memory_after:+.1f} MB memory freed")

            return gc_stat

        return None

    def get_gc_report(self):
        """Generate garbage collection report"""

        if not self.gc_stats:
            return {}

        total_collected = sum(stat['objects_collected'] for stat in self.gc_stats)
        total_memory_freed = sum(stat['memory_freed_mb'] for stat in self.gc_stats)
        avg_gc_interval = sum(stat['duration_seconds'] for stat in self.gc_stats) / len(self.gc_stats)

        return {
            'total_gc_cycles': len(self.gc_stats),
            'total_objects_collected': total_collected,
            'total_memory_freed_mb': total_memory_freed,
            'average_gc_interval_seconds': avg_gc_interval,
            'gc_efficiency': total_memory_freed / len(self.gc_stats) if self.gc_stats else 0
        }

# Global memory manager instance
memory_manager = MemoryManager()

def optimized_pipeline_stage(stage_func):
    """Decorator to add memory optimization to pipeline stages"""

    def wrapper(*args, **kwargs):
        # Pre-stage memory check
        memory_manager.perform_garbage_collection()

        # Execute stage
        result = stage_func(*args, **kwargs)

        # Post-stage cleanup
        memory_manager.perform_garbage_collection(force=True)

        return result

    return wrapper
```

## Computational Optimization

### Similarity Computation Optimization

**Vectorized Similarity Calculations**:
```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class OptimizedSimilarityComputer:
    """Optimized similarity computation using vectorization"""

    def __init__(self, use_gpu=False):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.use_gpu = use_gpu

        if use_gpu:
            try:
                import cupy as cp
                self.xp = cp
                logger.info("Using GPU acceleration for similarity computation")
            except ImportError:
                logger.warning("CuPy not available, falling back to CPU")
                self.use_gpu = False
                self.xp = np
        else:
            self.xp = np

    def fit_transform(self, texts):
        """Fit vectorizer and transform texts to TF-IDF matrix"""

        logger = logging.getLogger('performance.similarity')

        start_time = time.time()

        # Configure vectorizer for efficiency
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams
            max_features=10000,  # Limit features for memory efficiency
            min_df=2,  # Ignore terms appearing in less than 2 documents
            max_df=0.95  # Ignore terms appearing in more than 95% of documents
        )

        # Fit and transform
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

        # Convert to dense if using GPU
        if self.use_gpu:
            self.tfidf_matrix = csr_matrix(self.tfidf_matrix)  # Keep sparse for GPU transfer

        fit_time = time.time() - start_time
        matrix_shape = self.tfidf_matrix.shape
        matrix_size_mb = self.tfidf_matrix.data.nbytes / 1024 / 1024

        logger.info(f"TF-IDF matrix created: {matrix_shape[0]} documents, {matrix_shape[1]} features")
        logger.info(f"Matrix size: {matrix_size_mb:.1f} MB, fit time: {fit_time:.2f}s")

        return self.tfidf_matrix

    def compute_similarity_matrix(self, threshold=0.88):
        """Compute pairwise similarity matrix efficiently"""

        if self.tfidf_matrix is None:
            raise ValueError("Must call fit_transform first")

        logger = logging.getLogger('performance.similarity')
        start_time = time.time()

        n_docs = self.tfidf_matrix.shape[0]

        # For large matrices, use block-wise computation to save memory
        if n_docs > 1000:
            similarity_matrix = self._blockwise_similarity_computation(threshold)
        else:
            # Direct computation for smaller matrices
            similarity_matrix = cosine_similarity(self.tfidf_matrix)

            # Apply threshold
            similarity_matrix = np.where(similarity_matrix >= threshold, similarity_matrix, 0)

        computation_time = time.time() - start_time

        # Count similar pairs
        n_similar_pairs = np.sum((similarity_matrix >= threshold) & (np.triu(np.ones_like(similarity_matrix), k=1) == 1))

        logger.info(f"Similarity computation completed: {computation_time:.2f}s")
        logger.info(f"Found {n_similar_pairs} similar pairs above threshold {threshold}")

        return similarity_matrix

    def _blockwise_similarity_computation(self, threshold, block_size=500):
        """Compute similarity matrix in blocks to save memory"""

        n_docs = self.tfidf_matrix.shape[0]
        similarity_matrix = np.zeros((n_docs, n_docs))

        logger = logging.getLogger('performance.similarity')

        total_blocks = ((n_docs + block_size - 1) // block_size) ** 2
        block_count = 0

        for i in range(0, n_docs, block_size):
            i_end = min(i + block_size, n_docs)
            block_i = self.tfidf_matrix[i:i_end]

            for j in range(i, n_docs, block_size):  # Start from i to avoid duplicate computation
                j_end = min(j + block_size, n_docs)
                block_j = self.tfidf_matrix[j:j_end]

                # Compute block similarity
                block_similarity = cosine_similarity(block_i, block_j)

                # Apply threshold
                block_similarity = np.where(block_similarity >= threshold, block_similarity, 0)

                # Store in result matrix
                similarity_matrix[i:i_end, j:j_end] = block_similarity

                block_count += 1
                if block_count % 10 == 0:
                    logger.debug(f"Processed {block_count}/{total_blocks} blocks")

        return similarity_matrix

    def find_similar_pairs(self, similarity_matrix, threshold=0.88):
        """Extract similar pairs from similarity matrix efficiently"""

        # Find indices where similarity >= threshold
        # Use upper triangle only to avoid duplicates
        rows, cols = np.triu_indices_from(similarity_matrix, k=1)
        mask = similarity_matrix[rows, cols] >= threshold

        similar_pairs = list(zip(rows[mask], cols[mask], similarity_matrix[rows[mask], cols[mask]]))

        return similar_pairs
```

### Parallel Processing Implementation

**Multi-Core Task Processing**:
```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing as mp
from functools import partial

class ParallelProcessor:
    """Parallel processing utilities for pipeline optimization"""

    def __init__(self, max_workers=None, use_processes=True):
        self.max_workers = max_workers or mp.cpu_count()
        self.use_processes = use_processes

        # Choose executor type
        if use_processes:
            self.executor_class = ProcessPoolExecutor
            self.executor_kwargs = {'max_workers': self.max_workers, 'mp_context': mp.get_context('spawn')}
        else:
            self.executor_class = ThreadPoolExecutor
            self.executor_kwargs = {'max_workers': self.max_workers}

        self.executor = None

    def __enter__(self):
        self.executor = self.executor_class(**self.executor_kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.executor:
            self.executor.shutdown(wait=True)

    def map_function(self, func, items, chunk_size=None):
        """Map function over items in parallel"""

        if chunk_size is None:
            chunk_size = max(1, len(items) // (self.max_workers * 4))  # Adaptive chunking

        # Split items into chunks
        chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

        logger = logging.getLogger('performance.parallel')
        logger.info(f"Processing {len(items)} items in {len(chunks)} chunks of ~{chunk_size} items each")

        # Submit chunked tasks
        futures = []
        for chunk in chunks:
            future = self.executor.submit(self._process_chunk, func, chunk)
            futures.append(future)

        # Collect results
        results = []
        for future in futures:
            chunk_results = future.result()
            results.extend(chunk_results)

        return results

    def _process_chunk(self, func, chunk):
        """Process a chunk of items"""

        return [func(item) for item in chunk]

def parallel_similarity_computation(texts, threshold=0.88, max_workers=None):
    """Compute similarities in parallel"""

    logger = logging.getLogger('performance.similarity')

    n_texts = len(texts)
    logger.info(f"Computing similarities for {n_texts} texts using {max_workers or mp.cpu_count()} workers")

    # Create similarity computer
    sim_computer = OptimizedSimilarityComputer()

    # Fit vectorizer (single-threaded for now)
    sim_computer.fit_transform(texts)

    # For very large datasets, use block-wise parallel computation
    if n_texts > 2000:
        return parallel_blockwise_similarity(sim_computer, threshold, max_workers)
    else:
        # Direct computation
        similarity_matrix = sim_computer.compute_similarity_matrix(threshold)
        similar_pairs = sim_computer.find_similar_pairs(similarity_matrix, threshold)

        return similar_pairs

def parallel_blockwise_similarity(sim_computer, threshold, max_workers):
    """Compute similarities using parallel block processing"""

    n_docs = sim_computer.tfidf_matrix.shape[0]
    block_size = min(500, n_docs // max_workers) if max_workers else 500

    logger = logging.getLogger('performance.similarity')

    # Generate block coordinates
    blocks = []
    for i in range(0, n_docs, block_size):
        for j in range(i, n_docs, block_size):  # Upper triangle only
            blocks.append((i, min(i + block_size, n_docs), j, min(j + block_size, n_docs)))

    logger.info(f"Processing {len(blocks)} blocks in parallel")

    # Process blocks in parallel
    with ParallelProcessor(max_workers=max_workers) as processor:
        process_block_partial = partial(process_similarity_block,
                                      tfidf_matrix=sim_computer.tfidf_matrix,
                                      threshold=threshold)

        block_results = processor.map_function(process_block_partial, blocks)

    # Combine results
    all_similar_pairs = []
    for block_pairs in block_results:
        all_similar_pairs.extend(block_pairs)

    logger.info(f"Found {len(all_similar_pairs)} similar pairs across all blocks")

    return all_similar_pairs

def process_similarity_block(block_coords, tfidf_matrix, threshold):
    """Process a single similarity block"""

    i_start, i_end, j_start, j_end = block_coords

    # Extract block matrices
    block_i = tfidf_matrix[i_start:i_end]
    block_j = tfidf_matrix[j_start:j_end]

    # Compute similarities
    block_similarities = cosine_similarity(block_i, block_j)

    # Find similar pairs
    similar_pairs = []
    for ii in range(block_similarities.shape[0]):
        for jj in range(block_similarities.shape[1]):
            # Adjust indices for global matrix
            global_i = i_start + ii
            global_j = j_start + jj

            # Only include upper triangle pairs
            if global_i < global_j and block_similarities[ii, jj] >= threshold:
                similar_pairs.append((global_i, global_j, block_similarities[ii, jj]))

    return similar_pairs
```

### Caching and Memoization

**Computation Result Caching**:
```python
import functools
import hashlib
import pickle
from pathlib import Path

class ComputationCache:
    """Cache computation results to disk for reuse"""

    def __init__(self, cache_dir='cache', max_cache_size_gb=10):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_cache_size_gb = max_cache_size_gb

        # Clean old cache files if needed
        self._cleanup_cache()

    def cache_computation(self, func):
        """Decorator to cache function results"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = self._generate_cache_key(func.__name__, args, kwargs)

            # Check cache
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            if cache_file.exists():
                logger = logging.getLogger('performance.cache')
                logger.debug(f"Cache hit for {func.__name__}")

                try:
                    with open(cache_file, 'rb') as f:
                        return pickle.load(f)
                except Exception as e:
                    logger.warning(f"Cache read failed: {e}")
                    # Remove corrupted cache file
                    cache_file.unlink(missing_ok=True)

            # Compute result
            result = func(*args, **kwargs)

            # Cache result
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f)

                logger.debug(f"Cached result for {func.__name__}")
            except Exception as e:
                logger.warning(f"Cache write failed: {e}")

            return result

        return wrapper

    def _generate_cache_key(self, func_name, args, kwargs):
        """Generate unique cache key for function call"""

        # Create deterministic string representation
        key_data = {
            'func_name': func_name,
            'args': args,
            'kwargs': kwargs
        }

        # Hash the key data
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        cache_key = hashlib.sha256(key_str.encode()).hexdigest()[:16]

        return cache_key

    def _cleanup_cache(self):
        """Clean up old cache files if cache size exceeds limit"""

        cache_files = list(self.cache_dir.glob("*.pkl"))

        if not cache_files:
            return

        # Sort by modification time (oldest first)
        cache_files.sort(key=lambda x: x.stat().st_mtime)

        # Calculate total cache size
        total_size = sum(f.stat().st_size for f in cache_files)
        max_size_bytes = self.max_cache_size_gb * 1024**3

        # Remove oldest files until under limit
        removed_count = 0
        while total_size > max_size_bytes and cache_files:
            oldest_file = cache_files.pop(0)
            total_size -= oldest_file.stat().st_size
            oldest_file.unlink()
            removed_count += 1

        if removed_count > 0:
            logger = logging.getLogger('performance.cache')
            logger.info(f"Cache cleanup: removed {removed_count} old files")

# Global cache instance
computation_cache = ComputationCache()

# Example usage
@computation_cache.cache_computation
def compute_task_similarities(tasks_data, threshold=0.88):
    """Cached similarity computation"""

    # Implementation here
    return compute_similarities_uncached(tasks_data, threshold)
```

## I/O Optimization

### Batch File Operations

**Optimized File I/O**:
```python
import json
import csv
import gzip
import bz2
from typing import Iterator, List, Dict, Any

class OptimizedFileHandler:
    """Optimized file operations for large datasets"""

    @staticmethod
    def write_jsonl_gz(data: Iterator[Dict[str, Any]], filepath: str, batch_size: int = 1000):
        """Write data as compressed JSON Lines"""

        logger = logging.getLogger('performance.io')

        with gzip.open(filepath, 'wt', encoding='utf-8') as f:
            batch = []
            count = 0

            for item in data:
                batch.append(item)
                count += 1

                if len(batch) >= batch_size:
                    for item in batch:
                        json.dump(item, f)
                        f.write('\n')
                    batch = []

                    logger.debug(f"Written {count} items to {filepath}")

            # Write remaining items
            for item in batch:
                json.dump(item, f)
                f.write('\n')

        logger.info(f"Completed writing {count} items to {filepath}")

    @staticmethod
    def read_jsonl_gz(filepath: str) -> Iterator[Dict[str, Any]]:
        """Read compressed JSON Lines"""

        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    @staticmethod
    def write_csv_optimized(data: Iterator[Dict[str, Any]], filepath: str,
                          fieldnames: List[str], batch_size: int = 5000):
        """Write CSV with batching for performance"""

        logger = logging.getLogger('performance.io')

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            batch = []
            count = 0

            for row in data:
                batch.append(row)
                count += 1

                if len(batch) >= batch_size:
                    writer.writerows(batch)
                    batch = []
                    logger.debug(f"Written {count} rows to {filepath}")

            # Write remaining rows
            writer.writerows(batch)

        logger.info(f"Completed writing {count} rows to {filepath}")

    @staticmethod
    def stream_large_file(filepath: str, chunk_size: int = 8192) -> Iterator[str]:
        """Stream large file contents efficiently"""

        with open(filepath, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

class DataStreamer:
    """Stream processing for large datasets"""

    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size

    def stream_process_jobs(self, jobs_file: str) -> Iterator[List[Dict[str, Any]]]:
        """Stream and process jobs data in chunks"""

        logger = logging.getLogger('performance.io')

        jobs_chunk = []
        count = 0

        for job in OptimizedFileHandler.read_jsonl_gz(jobs_file):
            jobs_chunk.append(job)
            count += 1

            if len(jobs_chunk) >= self.chunk_size:
                logger.debug(f"Streaming chunk of {len(jobs_chunk)} jobs")
                yield jobs_chunk
                jobs_chunk = []

        # Yield remaining jobs
        if jobs_chunk:
            yield jobs_chunk

        logger.info(f"Streamed total of {count} jobs")

    def stream_process_tasks(self, tasks_data: Iterator[Dict[str, Any]]) -> Iterator[List[Dict[str, Any]]]:
        """Stream task processing to avoid loading all data in memory"""

        tasks_chunk = []

        for task in tasks_data:
            tasks_chunk.append(task)

            if len(tasks_chunk) >= self.chunk_size:
                yield tasks_chunk
                tasks_chunk = []

        if tasks_chunk:
            yield tasks_chunk
```

### Database Optimization

**Batch Database Operations**:
```python
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any

class OptimizedDatabaseHandler:
    """Optimized database operations for bulk data"""

    def __init__(self, db_path: str = 'soc_jobs.db'):
        self.db_path = db_path
        self._create_tables()

    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""

        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging for better concurrency
        conn.execute('PRAGMA synchronous=NORMAL')  # Balance performance and safety
        conn.execute('PRAGMA cache_size=-64000')  # 64MB cache

        try:
            yield conn
        finally:
            conn.close()

    def _create_tables(self):
        """Create optimized database schema"""

        with self.get_connection() as conn:
            # Jobs table with indexes
            conn.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY,
                    serpapi_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    company_name TEXT,
                    location TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tasks table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    job_id INTEGER,
                    task_text TEXT NOT NULL,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs(id)
                )
            ''')

            # Clusters table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clusters (
                    id INTEGER PRIMARY KEY,
                    representative_task TEXT NOT NULL,
                    task_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_name)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tasks_job_id ON tasks(job_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tasks_text ON tasks(task_text)')

    def bulk_insert_jobs(self, jobs_data: List[Dict[str, Any]]) -> int:
        """Bulk insert jobs with optimized performance"""

        logger = logging.getLogger('performance.db')

        with self.get_connection() as conn:
            # Prepare data
            job_records = []
            for job in jobs_data:
                job_records.append((
                    job.get('id'),
                    job.get('title', ''),
                    job.get('company_name'),
                    job.get('location'),
                    job.get('description', ''),
                ))

            # Bulk insert
            conn.executemany('''
                INSERT OR REPLACE INTO jobs
                (serpapi_id, title, company_name, location, description)
                VALUES (?, ?, ?, ?, ?)
            ''', job_records)

            inserted_count = len(job_records)
            conn.commit()

            logger.info(f"Bulk inserted {inserted_count} jobs")

            return inserted_count

    def bulk_insert_tasks(self, tasks_data: List[Dict[str, Any]]) -> int:
        """Bulk insert tasks with optimized performance"""

        logger = logging.getLogger('performance.db')

        with self.get_connection() as conn:
            # Prepare data
            task_records = []
            for task in tasks_data:
                task_records.append((
                    task.get('job_id'),
                    task.get('text', ''),
                    task.get('confidence', 0.0),
                ))

            # Bulk insert
            conn.executemany('''
                INSERT INTO tasks (job_id, task_text, confidence)
                VALUES (?, ?, ?)
            ''', task_records)

            inserted_count = len(task_records)
            conn.commit()

            logger.info(f"Bulk inserted {inserted_count} tasks")

            return inserted_count

    def get_jobs_iterator(self, batch_size: int = 1000) -> Iterator[List[Dict[str, Any]]]:
        """Get jobs in batches for memory-efficient processing"""

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM jobs ORDER BY id')

            batch = []
            for row in cursor:
                job_dict = {
                    'id': row[0],
                    'serpapi_id': row[1],
                    'title': row[2],
                    'company_name': row[3],
                    'location': row[4],
                    'description': row[5],
                }
                batch.append(job_dict)

                if len(batch) >= batch_size:
                    yield batch
                    batch = []

            if batch:
                yield batch

    def optimize_database(self):
        """Optimize database for query performance"""

        logger = logging.getLogger('performance.db')

        with self.get_connection() as conn:
            # Analyze tables for query optimization
            conn.execute('ANALYZE')

            # Vacuum for space optimization
            conn.execute('VACUUM')

            logger.info("Database optimization completed")
```

## Performance Monitoring and Profiling

### Real-Time Performance Monitoring

**Performance Metrics Collector**:
```python
import time
from collections import deque
import threading

class PerformanceMonitor:
    """Real-time performance monitoring for pipeline stages"""

    def __init__(self, window_size=100):
        self.metrics = {}
        self.window_size = window_size
        self.lock = threading.Lock()

    def record_metric(self, stage_name: str, metric_name: str, value: float):
        """Record a performance metric"""

        with self.lock:
            if stage_name not in self.metrics:
                self.metrics[stage_name] = {}

            if metric_name not in self.metrics[stage_name]:
                self.metrics[stage_name][metric_name] = deque(maxlen=self.window_size)

            self.metrics[stage_name][metric_name].append({
                'value': value,
                'timestamp': time.time()
            })

    def get_stage_metrics(self, stage_name: str) -> Dict[str, Any]:
        """Get performance metrics for a stage"""

        with self.lock:
            if stage_name not in self.metrics:
                return {}

            stage_metrics = {}
            for metric_name, values in self.metrics[stage_name].items():
                if values:
                    metric_values = [v['value'] for v in values]
                    stage_metrics[metric_name] = {
                        'current': metric_values[-1],
                        'average': sum(metric_values) / len(metric_values),
                        'min': min(metric_values),
                        'max': max(metric_values),
                        'count': len(metric_values)
                    }

            return stage_metrics

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics"""

        with self.lock:
            return {
                stage: self.get_stage_metrics(stage)
                for stage in self.metrics.keys()
            }

# Global performance monitor
performance_monitor = PerformanceMonitor()

def monitored_stage(stage_name):
    """Decorator to monitor pipeline stage performance"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

                # Record metrics
                duration = end_time - start_time
                memory_delta = end_memory - start_memory

                performance_monitor.record_metric(stage_name, 'duration_seconds', duration)
                performance_monitor.record_metric(stage_name, 'memory_delta_mb', memory_delta)
                performance_monitor.record_metric(stage_name, 'cpu_percent',
                    psutil.Process(os.getpid()).cpu_percent())

                logger = logging.getLogger('performance.monitor')
                logger.info(f"Stage '{stage_name}' completed: {duration:.2f}s, "
                           f"memory Δ{memory_delta:+.1f} MB")

        return wrapper
    return decorator
```

### Automated Performance Optimization

**Adaptive Configuration Tuning**:
```python
class PerformanceOptimizer:
    """Automated performance optimization based on system characteristics"""

    def __init__(self):
        self.system_info = self._get_system_info()

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system performance characteristics"""

        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_logical_count': psutil.cpu_count(logical=True),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3),
            'available_memory_gb': psutil.virtual_memory().available / (1024**3),
            'cpu_freq_mhz': psutil.cpu_freq().max if psutil.cpu_freq() else 0,
        }

    def recommend_configuration(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend optimized configuration based on system capabilities"""

        optimized_config = pipeline_config.copy()

        # Memory-based recommendations
        memory_gb = self.system_info['total_memory_gb']

        if memory_gb < 8:
            # Low memory system
            optimized_config['performance'] = {
                'max_workers': min(2, self.system_info['cpu_count']),
                'memory_limit_mb': 1024,
                'batch_size': 500
            }
            optimized_config['task_aggregation'] = {
                'processing_batch_size': 500,
                'similarity_threshold': 0.9  # Higher threshold for fewer comparisons
            }
        elif memory_gb < 16:
            # Medium memory system
            optimized_config['performance'] = {
                'max_workers': min(4, self.system_info['cpu_count']),
                'memory_limit_mb': 2048,
                'batch_size': 1000
            }
        else:
            # High memory system
            optimized_config['performance'] = {
                'max_workers': min(8, self.system_info['cpu_logical_count']),
                'memory_limit_mb': 4096,
                'batch_size': 2000
            }

        # CPU-based recommendations
        cpu_count = self.system_info['cpu_count']

        if cpu_count >= 8:
            # Multi-core system optimizations
            optimized_config['performance']['parallel_processing'] = True
        else:
            # Single-core optimizations
            optimized_config['performance']['parallel_processing'] = False

        return optimized_config

    def monitor_and_adapt(self, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor performance and suggest adaptations"""

        adaptations = {}

        # Check memory pressure
        if current_metrics.get('memory_percent', 0) > 85:
            adaptations['reduce_batch_size'] = True
            adaptations['increase_gc_frequency'] = True

        # Check CPU utilization
        if current_metrics.get('cpu_percent', 0) > 95:
            adaptations['reduce_workers'] = True

        # Check processing speed
        avg_duration = current_metrics.get('avg_stage_duration', 0)
        if avg_duration > 300:  # 5 minutes per stage
            adaptations['optimize_similarity_algorithm'] = True

        return adaptations

# Global optimizer instance
performance_optimizer = PerformanceOptimizer()
```

This comprehensive performance optimization guide provides practical strategies for improving SOC Job Task Analyzer efficiency across memory management, computation, I/O operations, and parallel processing, with automated monitoring and adaptive configuration capabilities.

---

**Last Updated:** December 2024
**Version:** 1.0.0