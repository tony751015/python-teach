<template>
  <v-dialog v-model="uploadImage" max-width="600px">
    <v-card class="upload-image-dialog">
      <v-card-title>
        Upload Image
      </v-card-title>
      <v-card-text>
        <v-file-input
          label="Select an image"
          v-model="image"
          :rules="[rules.required, rules.size, rules.type]"
        />
        <v-alert v-if="error" type="error">
          {{ error }}
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeUploadImage">
          Close
        </v-btn>
        <v-btn color="blue darken-1" text @click="toUploadImage">
          Upload
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      uploadImage: true,
      image: null,
      error: null,
      rules: {
        required: (value) => !!value || "Please select an image",
        size: (value) =>
          !value || value.size < 8000000 || "Image size should be less than 8MB",
        type: (value) =>
          !value || value.type === "image/jpeg" || value.type === "image/png" || "Only JPEG and PNG images are allowed",
      },
    };
  },
  methods: {
      closeUploadImage() {
      this.uploadImage = false;
    },
    toUploadImage() {
      if (this.image) {
        // Upload image logic here
        console.log("Uploading image:", this.image);
        this.closeDialog();
      } else {
        this.error = "Please select an image";
      }
    },
  },
};
</script>