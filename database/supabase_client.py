"""
Supabase client configuration for Luna AI
Free tier: 500MB PostgreSQL + Authentication + Real-time
"""
import os
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta


class SupabaseClient:
    """Supabase client wrapper for Luna AI"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_ANON_KEY", "")

        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables required")

        self.client: Client = create_client(self.url, self.key)
        self.auth = self.client.auth
        self.db = self.client.table

    def create_user_profile(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user profile in Supabase"""
        try:
            result = (self.db("user_profiles")
                     .insert(user_data)
                     .execute())
            return result.data if result.data else {}
        except Exception as e:
            logging.error(f"Error creating user profile: {e}")
            raise

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from Supabase"""
        try:
            result = (self.db("user_profiles")
                     .select("*")
                     .eq("id", user_id)
                     .execute())
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"Error fetching user profile: {e}")
            return None

    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            updates["updated_at"] = datetime.utcnow().isoformat()
            result = (self.db("user_profiles")
                     .update(updates)
                     .eq("id", user_id)
                     .execute())
            return result.data if result.data else {}
        except Exception as e:
            logging.error(f"Error updating user profile: {e}")
            raise

    def save_memory_context(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save memory context to Supabase"""
        try:
            memory_data["created_at"] = datetime.utcnow().isoformat()
            result = (self.db("memory_contexts")
                     .insert(memory_data)
                     .execute())
            return result.data if result.data else {}
        except Exception as e:
            logging.error(f"Error saving memory context: {e}")
            raise

    def get_user_memory(self, user_id: str, context_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user memory contexts"""
        try:
            query = (self.db("memory_contexts")
                    .select("*")
                    .eq("user_id", user_id)
                    .eq("is_active", True)
                    .order("updated_at", desc=True)
                    .limit(limit))

            if context_type:
                query = query.eq("context_type", context_type)

            result = query.execute()
            return result.data or []
        except Exception as e:
            logging.error(f"Error fetching user memory: {e}")
            return []

    def save_interaction(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user interaction"""
        try:
            interaction_data["created_at"] = datetime.utcnow().isoformat()
            result = (self.db("user_interactions")
                     .insert(interaction_data)
                     .execute())
            return result.data if result.data else {}
        except Exception as e:
            logging.error(f"Error saving interaction: {e}")
            raise

    def get_user_interactions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user interaction history"""
        try:
            result = (self.db("user_interactions")
                     .select("*")
                     .eq("user_id", user_id)
                     .order("created_at", desc=True)
                     .limit(limit)
                     .execute())
            return result.data or []
        except Exception as e:
            logging.error(f"Error fetching user interactions: {e}")
            return []

    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user analytics from interactions"""
        try:
            # Get all interactions for analytics
            interactions = (self.db("user_interactions")
                           .select("query_type, confidence, created_at")
                           .eq("user_id", user_id)
                           .execute()).data

            if not interactions:
                return {"user_id": user_id, "total_interactions": 0}

            # Calculate analytics
            total_interactions = len(interactions)
            avg_confidence = sum(i["confidence"] for i in interactions) / total_interactions

            query_type_distribution = {}
            for interaction in interactions:
                qt = interaction["query_type"]
                query_type_distribution[qt] = query_type_distribution.get(qt, 0) + 1

            return {
                "user_id": user_id,
                "total_interactions": total_interactions,
                "average_confidence": round(avg_confidence, 2),
                "query_type_distribution": query_type_distribution,
                "last_interaction": interactions[0]["created_at"] if interactions else None
            }
        except Exception as e:
            logging.error(f"Error calculating user analytics: {e}")
            return {"error": str(e)}


# Global Supabase client instance
supabase_client = SupabaseClient()
