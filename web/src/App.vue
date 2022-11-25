<template>
  <n-config-provider :theme="darkTheme">
    <n-card>
        <div style="text-align: center">
            <h1 style="margin: 0">Проект "Тарантино"</h1>
            <h3 style="font-style: italic; font-weight: 300; margin: 0">by "Криминальное тестирование"</h3>
        </div>
    </n-card>

    <n-card style="margin-top: 12px;">
        <h3 style="text-align: center; font-weight: 300; margin-top: 0">Анализируемый репозиторий:</h3>

        <n-input
            value="https://github.com/angular/angular"
            disabled
        />
    </n-card>

    <n-card style="margin-top: 12px;">
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

const API = "http://83.222.10.235:5000"

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
        error.value = err?.response?.data || "Всё плохо, произошла ошибка..."
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
