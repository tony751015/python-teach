<template>
  <div class="error500">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>500 Internal Server Error</h1>
          <p>Sorry, something went wrong on our end.</p>
          <button @click="$router.push('/')">Back to Home</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error500'
}
</script>

<style scoped>
.error500 {
  background-image: url(../assets/loginBG.png);
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

p {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>