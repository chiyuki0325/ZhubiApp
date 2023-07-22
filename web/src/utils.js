import {HmacSHA256, enc as cryptoEnc} from 'crypto-js'
import {key, apiUrl} from '@/config/config'
import axios from 'axios'

export function calculatePasswordHash(password) {
  return HmacSHA256(password, key).toString(cryptoEnc.Hex)
}

export const api = {
  // 对 axios 的封装
  get: (url, params) => {
    return axios.get(apiUrl + url, {params})
  },
  post: (url, data) => {
    return axios.post(apiUrl + url, data)
  }
}
