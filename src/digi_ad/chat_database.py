from supabase import create_client, Client
import os
SUPABASE_URL =os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_chat_history(user_id: str) -> str:
    if not user_id:
        return ""
    
    try:
        response = supabase.table("digi-ad-chat-messages") \
                           .select("user_message, bot_message") \
                           .eq("user_id", user_id) \
                           .order("created_at") \
                           .execute()

        if response.data:
            return "\n".join(
                [f"User: {msg['user_message']}\nBot: {msg['bot_message']}" 
                 for msg in response.data]
            )
        return ""
        
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return ""


def save_message(user_id, session_id, user_message, bot_message):
    data = {
        "user_id": user_id,
        "session_id": session_id,
        "user_message": user_message,
        "bot_message": bot_message,
    }
    response = supabase.table("digi-ad-chat-messages").insert(data).execute()
    return response

