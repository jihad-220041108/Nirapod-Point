import { createClient } from '@supabase/supabase-js';
import Constants from 'expo-constants';
import { supabaseStorage } from './supabase-storage';

// Get Supabase credentials from environment variables
const SUPABASE_URL =
  Constants.expoConfig?.extra?.supabaseUrl || 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY =
  Constants.expoConfig?.extra?.supabaseAnonKey || 'YOUR_SUPABASE_ANON_KEY';

// Create Supabase client with SecureStore for session persistence
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: supabaseStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
