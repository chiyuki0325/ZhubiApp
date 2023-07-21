import {HmacSHA256, enc as cryptoEnc} from 'crypto-js'
import {key} from '@/config/config'

export function calculatePasswordHash(password) {
  return HmacSHA256(password, key).toString(cryptoEnc.Hex)
}
