import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Custom storage adapter for Supabase to use AsyncStorage
 * Note: Supabase session data can exceed 2048 bytes (SecureStore limit)
 * so we use AsyncStorage instead. Tokens are separately stored in SecureStore.
 */
export const supabaseStorage = {
  async getItem(key: string): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(key);
    } catch (error) {
      console.error('Error getting item from AsyncStorage:', error);
      return null;
    }
  },

  async setItem(key: string, value: string): Promise<void> {
    try {
      await AsyncStorage.setItem(key, value);
    } catch (error) {
      console.error('Error setting item in AsyncStorage:', error);
    }
  },

  async removeItem(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing item from AsyncStorage:', error);
    }
  },
};
