import { defineStore } from 'pinia'
import { getPriceTrend, getPriceCompare, getAlertList, getPrediction } from '@/api/price'

export const usePriceStore = defineStore('price', {
  state: () => ({
    trendData: [],
    compareData: [],
    alertList: [],
    predictionData: [],
    loading: false
  }),
  
  actions: {
    async fetchTrend({ commit }, { productId, regionId, startDate, endDate }) {
      commit('SET_LOADING', true)
      try {
        const response = await getPriceTrend({ productId, regionId, startDate, endDate })
        commit('SET_TREND_DATA', response.data)
        return { success: true }
      } catch (error) {
        commit('SET_LOADING', false)
        return { success: false, message: error.message }
      }
    },
    
    async fetchCompare({ commit }, { productId, regionIds, date }) {
      commit('SET_LOADING', true)
      try {
        const response = await getPriceCompare({ productId, regionIds, date })
        commit('SET_COMPARE_DATA', response.data)
        return { success: true }
      } catch (error) {
        commit('SET_LOADING', false)
        return { success: false, message: error.message }
      }
    },
    
    async fetchAlerts({ commit }, params) {
      commit('SET_LOADING', true)
      try {
        const response = await getAlertList(params)
        commit('SET_ALERT_LIST', response.data)
        return { success: true }
      } catch (error) {
        commit('SET_LOADING', false)
        return { success: false, message: error.message }
      }
    },
    
    async fetchPrediction({ commit }, { productId, regionId, predictDays }) {
      commit('SET_LOADING', true)
      try {
        const response = await getPrediction({ productId, regionId, predictDays })
        commit('SET_PREDICTION_DATA', response.data)
        return { success: true }
      } catch (error) {
        commit('SET_LOADING', false)
        return { success: false, message: error.message }
      }
    }
  },
  
  mutations: {
    SET_TREND_DATA(state, data) {
      state.trendData = data
      state.loading = false
    },
    
    SET_COMPARE_DATA(state, data) {
      state.compareData = data
      state.loading = false
    },
    
    SET_ALERT_LIST(state, data) {
      state.alertList = data
      state.loading = false
    },
    
    SET_PREDICTION_DATA(state, data) {
      state.predictionData = data
      state.loading = false
    },
    
    SET_LOADING(state(state, loading) {
      state.loading = loading
    }
  }
})
