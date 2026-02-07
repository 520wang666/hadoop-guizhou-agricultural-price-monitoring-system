import { defineStore } from 'pinia'
import { login as loginApi, logout as logoutApi } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
    userId: localStorage.getItem('userId') || '',
    role: localStorage.getItem('role') || ''
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await loginApi({ username, password })
        const { token, userInfo } = response.data
        
        commit('SET_TOKEN', token)
        commit('SET_USER_INFO', userInfo)
        
        return { success: true }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },
    
    async logout({ commit }) {
      try {
        await logoutApi()
        commit('CLEAR_USER')
        return { success: true }
      } catch (error) {
        return { success: false, message: error.message }
      }
    }
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    
    SET_USER_INFO(state, userInfo) {
      state.username = userInfo.username
      state.userId = userInfo.userId
      state.role = userInfo.role
      localStorage.setItem('username', userInfo.username)
      localStorage.setItem('userId', userInfo.userId)
      localStorage.setItem('role', userInfo.role)
    },
    
    CLEAR_USER(state) {
      state.token = ''
      state.username = ''
      state.userId = ''
      state.role = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('userId')
      localStorage.removeItem('role')
    }
  }
})
