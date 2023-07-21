import {HmacSHA256, enc as cryptoEnc} from 'crypto-js'

export function calculatePasswordHash(password) {
  return HmacSHA256(password, '6634409710').toString(cryptoEnc.Hex)
}
