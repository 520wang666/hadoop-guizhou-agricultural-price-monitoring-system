<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header">
          <h1>农产品价格监测系统</h1>
          <div class="user-info" v-if="isLoggedIn">
            <el-dropdown>
              <span class="el-dropdown-link">
                {{ username }}
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </template>
            </el-dropdown>
          </div>
          <div class="user-info" v-else>
            <el-button type="primary" @click="handleLogin">登录</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const username = computed(() => userStore.username)

const handleLogin = () => {
  router.push('/login')
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
#app {
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  background: #409eff;
  color: white;
}

.header h1 {
  margin: 0;
  font-size: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  color: white;
}
</style>
