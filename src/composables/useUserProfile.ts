import { ref, computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import type { UserProfile } from '../types/user'

export function useUserProfile(username: string) {
  const query = useQuery<UserProfile>({
    queryKey: ['userProfile', username],
    queryFn: async () => {
      const { data } = await axios.get<UserProfile>(`/api/user/${username}`)
      return data
    },
    enabled: computed(() => !!username),
    staleTime: 5 * 60 * 1000, 
    retry: 1,
  })

  return {
    user: query.data,
    isLoading: query.isLoading,
    error: query.error,
    refetch: query.refetch,
  }
}