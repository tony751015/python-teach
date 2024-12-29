<template>
  <div class="error404">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>404 Not Found</h1>
          <p>Sorry, the page you are looking for does not exist.</p>
          <button @click="$router.push('/')">Back to Home</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error404'
}
</script>

<style scoped>
.error404 {
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
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

p {
  font-size: 18px;
  margin-bottom: 20px;
}

button {
  background-color: #4CAF50;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #3e8e41;
}
</style>