<template>
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <button class="close-button" @click="$emit('close')">×</button>
        
        <div class="auth-forms">
          <!-- 登录表单 -->
          <form @submit.prevent="handleLogin" class="auth-form">
            <h2>Login</h2>
            <input type="text" placeholder="Username" required v-model="loginForm.username">
            <input type="password" placeholder="Password" required v-model="loginForm.password">
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <button type="submit" class="auth-button">Login</button>
          </form>
  
          <div class="divider">OR</div>
  
          <!-- 注册表单 -->
          <form @submit.prevent="handleRegister" class="auth-form">
            <h2>Register</h2>
            <input type="text" placeholder="Username" required v-model="registerForm.username">
            <input type="password" placeholder="Password" required v-model="registerForm.password">
            <input type="text" placeholder="Invitation Code" required v-model="registerForm.invitation_code">
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <button type="submit" class="auth-button">Register</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isOpen: Boolean
    },
    data() {
      return {
        loginForm: {
          username: '',
          password: ''
        },
        registerForm: {
          username: '',
          password: '',
          invitation_code: ''
        },
        errorMessage: ''
      };
    },
    methods: {
      async handleLogin() {
        try {
          // 构造符合OAuth2规范的表单数据
          const formData = new URLSearchParams();
          formData.append('username', this.loginForm.username);
          formData.append('password', this.loginForm.password);
  
          const response = await fetch('/api/token', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
          }
  
          const { access_token } = await response.json();
          localStorage.setItem('access_token', access_token);
          this.$emit('login-success');
          this.errorMessage = '';
        } catch (error) {
          this.errorMessage = error.message;
          this.loginForm.password = '';
        }
      },
  
      async handleRegister() {
        try {
          const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.registerForm.username,
              password: this.registerForm.password,
              invitation_code: this.registerForm.invitation_code
            })
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Registration failed');
          }
  
          // 注册成功后自动登录
          await this.handleLogin();
        } catch (error) {
          this.errorMessage = error.message;
          this.registerForm.password = '';
          this.registerForm.invitation_code = '';
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .modal-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    width: 400px;
    position: relative;
  }
  
  .close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
  }
  
  .auth-forms {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .auth-button {
    padding: 0.5rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .auth-button:hover {
    background: #0056b3;
  }
  
  .divider {
    text-align: center;
    position: relative;
    color: #666;
  }
  
  .divider::before,
  .divider::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 45%;
    height: 1px;
    background: #ddd;
  }
  
  .divider::before {
    left: 0;
  }
  
  .divider::after {
    right: 0;
  }
  
  .error-message {
    color: #dc3545;
    font-size: 0.9rem;
    text-align: center;
    padding: 0.5rem;
    background: #f8d7da;
    border-radius: 4px;
    border: 1px solid #f5c6cb;
  }
  </style>