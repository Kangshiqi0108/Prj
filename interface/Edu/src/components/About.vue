<template>
  <div class="content">
    <h1>Grouping page</h1>
    <p>Page for performing grouping tasks.</p>
    <div>
      <h2>Select Importance and Group Type for Each Criterion</h2>
      
      <!-- Learning Ability -->
      <div>
        <h3>Learning Ability</h3>
        <label>
          Importance: 
          <select v-model="criteria.capability.importance">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.capability.groupType" value="homogeneous" />
          Homogeneous (Same)
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.capability.groupType" value="heterogeneous" />
          Heterogeneous (Different)
        </label>
      </div>

      <!-- Gender -->
      <div>
        <h3>Gender</h3>
        <label>
          Importance: 
          <select v-model="criteria.gender.importance">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.gender.groupType" value="homogeneous" />
          Homogeneous (Same)
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.gender.groupType" value="heterogeneous" />
          Heterogeneous (Different)
        </label>
      </div>

      <!-- Learning Style -->
      <div>
        <h3>Learning Style</h3>
        <label>
          Importance: 
          <select v-model="criteria.style.importance">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.style.groupType" value="homogeneous" />
          Homogeneous (Same)
        </label>
        <br />
        <label>
          <input type="radio" v-model="criteria.style.groupType" value="heterogeneous" />
          Heterogeneous (Different)
        </label>
      </div>

      <button @click="sendGrouping">Submit</button>
      <p v-if="message">{{ message }}</p>

      <!-- 新增的展示返回结果的部分 -->
      <div v-if="showResults">
        <h2>Grouping Results</h2>
        <table>
          <thead>
            <tr>
              <th>Group Number</th>
              <th>Group Members</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(group, index) in groupedResults" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ group.join(', ') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';

export default {
  name: 'About',
  setup() {
    const criteria = reactive({
      capability: {
        importance: 5,
        groupType: 'homogeneous'
      },
      gender: {
        importance: 5,
        groupType: 'homogeneous'
      },
      style: {
        importance: 5,
        groupType: 'homogeneous'
      }
    });
    const message = ref('');
    const showResults = ref(false);
    const groupedResults = ref([]);

    const sendGrouping = async () => {
      const data = Object.keys(criteria).map(key => ({
        criterion: key,
        importance: criteria[key].importance,
        group_type: criteria[key].groupType
      }));

      try {
        const response = await fetch('/api/grouping/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
          message.value = `Groups created successfully`;
          console.log(result.groups);
          // 处理返回的结果
          groupedResults.value = Object.values(result.groups);
          showResults.value = true;
        } else {
          message.value = result.error || 'An error occurred while sending the request.';
          showResults.value = false;
        }
      } catch (error) {
        message.value = `Error: ${error.message}`;
        showResults.value = false;
      }
    };

    return {
      criteria,
      sendGrouping,
      message,
      showResults,
      groupedResults
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
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

label {
  display: block;
  margin-bottom: 10px;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}
</style>