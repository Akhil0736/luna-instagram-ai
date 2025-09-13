import asyncio
from cache_manager import enhanced_cache_manager
from ai_client import call_openrouter_model, detect_query_type, select_luna_model

async def test_caching():
    # Initialize cache
    await enhanced_cache_manager.init_redis()
    
    # Test query
    query = "Hi, how are you?"
    query_type = detect_query_type(query)
    model = select_luna_model(query, query_type)
    
    print(f"Query: {query}")
    print(f"Type: {query_type}")
    print(f"Model: {model}")
    
    # Generate cache key
    cache_key = enhanced_cache_manager.generate_cache_key(query, model)
    print(f"Cache key: {cache_key[:16]}...")
    
    # Check cache (should be miss first time)
    cached = await enhanced_cache_manager.get_cached_response(cache_key)
    print(f"Cache result: {'HIT' if cached else 'MISS'}")
    
    # Get stats
    stats = enhanced_cache_manager.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    await enhanced_cache_manager.close()

if __name__ == "__main__":
    asyncio.run(test_caching())
