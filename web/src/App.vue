<template>
  <n-config-provider :theme="darkTheme">
    <n-card>
      <n-space vertical>
        <n-select
            :options="authors_options"
            v-model:value="author"
        />
        <n-input
            v-model:value="msg"
            placeholder="Сообщение"
        />
        <n-input
            v-model:value="file"
            placeholder="Файл"
        />
        <n-date-picker
            v-model:value="date"
        />

        <n-button type="primary" block @click="onClickSubmit">Отправить</n-button>
      </n-space>
    </n-card>

    <n-card style="margin-top: 12px;" v-if="result || error">
      <div style="text-align: center" v-if="result">
        Вероятность того, что коммит окажется "ломающим"
        <br>
        <h1>
          {{ result.toFixed(4) }}
        </h1>
        <br>
        <div>
          Для ревьюю рекомендуется {{person}}
        </div>
      </div>
      <div v-else style="text-align: center; color: red">
        {{ error }}
      </div>
    </n-card>
  </n-config-provider>
</template>

<script setup>
import {NInput, NButton, NSelect, NCard, darkTheme, NConfigProvider} from 'naive-ui'
import {authors} from "./authors.js"
import {computed, ref} from "vue"
import axios from "axios"

const authors_options = computed(() => {

  return authors.sort(() => true).map(a => {
    const ar = a.split(" ")
    const name = ar.slice(0, ar.length - 1).join(" ")

    return {label: a, value: name}
  })
})

const API = "http://localhost:5000"

const author = ref("Alex Rickabaugh")
const msg = ref("update package.json file")
const file = ref("package.json")
const date = ref(new Date().getTime())

const result = ref(0)
const person = ref("")
const error = ref("")

const onClickSubmit = () => {
  axios.post(API + "/api/predict", {
    "file": [file.value],
    "author": [author.value],
    "msg": [msg.value],
    "date": [Math.trunc(date.value / 1000)]
  })
      .then((res) => {
        result.value = res.data.result
        person.value = res.data.person
      })
      .catch((err) => {
        error.value = err.response.data
        result.value = ""
      })
}

</script>

<style>
body {
  background: #212121;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
