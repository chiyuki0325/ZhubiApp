import {HmacSHA256, enc as cryptoEnc} from 'crypto-js'
import {key, apiUrl} from '@/config/config'
import axios from 'axios'
import Cookies from 'js-cookie'

export function calculatePasswordHash(password) {
  return HmacSHA256(password, key).toString(cryptoEnc.Hex)
}

export const api = axios.create({
  baseURL: apiUrl,
})

export const useAuth = () => ({
  headers: {
    Authorization: `Bearer ${Cookies.get('token')}`,
  }
})

export function mediaUrl(fileId) {
  if (fileId) {
    return `${apiUrl}/misc/media/${fileId}`
  } else {
    return '/assets/telegram.png'
  }
}

export function isShowChat(chatType, tab) {
  switch (tab) {
    case 'all': return true
    case 'group': return chatType === 'group' || chatType === 'supergroup'
    case 'channel': return chatType === 'channel'
    case 'private': return chatType === 'private'
    case 'bot': return chatType === 'bot'
  }
}

export function prettifyName(user) {
  if (!user) return ''
  return (user.first_name + ' ' + (user.last_name || '')).trim()
}
