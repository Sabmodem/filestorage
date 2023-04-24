<template>
  <div class="container">
    <div class="d-flex justify-content-center">
      <div class="d-flex flex-column">
        <div class="d-flex justify-content-center">
          <h1>Загрузить файл:</h1>
        </div>
        <form id="muf" class="dropzone"></form>
      </div>
    </div>
    <div class="mt-3">
      <div clas="row">
        <div class="col text-center">
          <h1>Доступные файлы:</h1>
        </div>
      </div>
      <div clas="row" v-if="files.length == 0">
        <div class="col text-center">
          <h1>Нет файлов</h1>
        </div>
      </div>
      <div v-for="file in files">
        <div class="row">
          <div class="col-md-6 text-center">
            <label>{{ file.filename }}</label>
          </div>
          <div class="col-md-6 text-center">
            <a title="Скачать" class="btn btn-outline-primary" :href="`/files/${file.filename}`" download><i
                class="bi bi-file-earmark-arrow-down"></i></a>
            <button title="Удалить" class="btn btn-outline-danger" @click="deleteFile(file)"><i
                class="bi bi-trash3"></i></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Dropzone from 'dropzone';
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      files: [],
      uploadProgress: null
    };
  },
  methods: {
    async getFilesList() {
      const files = await axios.get('/files');
      this.files = files.data;
    },
    async deleteFile(file) {
      const result = await Swal.fire({
        title: 'Вы уверены, что хотите удалить этот файл?',
        showCancelButton: true,
        confirmButtonText: 'Удалить',
      });
      if (result.isConfirmed) {
        await axios.delete(`/files/${file.filename}`);
        await this.getFilesList();
        await Swal.fire('Данные удалены', '', 'success');
      };
    },
    viewFile(file) {
      window.open(`/static/uploads/${file.filename}`);
    }
  },
  async mounted() {
    await this.getFilesList();
    const dz = new Dropzone("form#muf", {
      url: "/files",
      method: 'post',
      maxFilesize: 1024,
      uploadMultiple: true,
      createImageThumbnails: false
    });
    dz.on("totaluploadprogress", (progress) => this.uploadProgress = progress.toFixed());
    dz.on("success", async (file) => await this.getFilesList());
  }
}
</script>
