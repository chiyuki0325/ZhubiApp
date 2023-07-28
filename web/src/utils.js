import {HmacSHA256, enc as cryptoEnc} from 'crypto-js'
import {key, apiUrl} from '@/config/config'
import axios from 'axios'

export function calculatePasswordHash(password) {
  return HmacSHA256(password, key).toString(cryptoEnc.Hex)
}

export const api = axios.create({
  baseURL: apiUrl,
})
