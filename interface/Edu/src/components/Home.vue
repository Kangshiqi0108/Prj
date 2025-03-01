<template>
  <div class="content">
    <h1>Update page</h1>
    <p>Update learner information through Excel chart.</p>
    <div>
      <h2>Upload File</h2>
      <input type="file" @change="handleFileChange" accept=".xlsx" />
      <button @click="uploadFile">Upload</button>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Home',
  setup() {
    const file = ref(null);
    const message = ref('');

    const handleFileChange = (event) => {
      file.value = event.target.files[0];
    };

    const uploadFile = async () => {
      if (!file.value) {
        message.value = 'Please select a file first.';
        return;
      }

      const formData = new FormData();
      formData.append('file', file.value);

      try {
        // Ensure the path matches exactly with the backend route
        const response = await fetch('/api/uploadfile/', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        if (response.ok) {
          message.value = result.message;
        } else {
          message.value = result.error || 'An error occurred while uploading the file.';
        }
      } catch (error) {
        message.value = `Error: ${error.message}`;
      }
    };

    return {
      handleFileChange,
      uploadFile,
      message
    };
  }
};
</script>

<style scoped>
.content {
  padding: 15px;
  flex-grow: 1;
}

button {
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

input[type="file"] {
  margin-bottom: 10px;
}
</style>