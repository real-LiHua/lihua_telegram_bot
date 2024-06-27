"use strict";
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/* Block TEA (xxtea) Tiny Encryption Algorithm                        (c) Chris Veness 2002-2018  */

/*                                                                                   MIT Licence  */

/* www.movable-type.co.uk/scripts/tea-block.html                                                  */

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/**
 * Tiny Encryption Algorithm. David Wheeler & Roger Needham, Cambridge University Computer Lab.
 *
 * www.movable-type.co.uk/scripts/tea.pdf   - TEA, a Tiny Encryption Algorithm (1994)
 * www.movable-type.co.uk/scripts/xtea.pdf  - Tea extensions (1997)
 * www.movable-type.co.uk/scripts/xxtea.pdf - Correction to xtea (1998)
 */
function strToLongs(s) {
      // note chars must be within ISO-8859-1 (Unicode code-point <= U+00FF) to fit 4/long
      var l = new Array(Math.ceil(s.length / 4));

      for (var i = 0; i < l.length; i++) {
        l[i] = s.charCodeAt(i * 4) + (s.charCodeAt(i * 4 + 1) << 8) + (s.charCodeAt(i * 4 + 2) << 16) + (s.charCodeAt(i * 4 + 3) << 24);
      } // note running off the end of the string generates nulls since bitwise operators treat NaN as 0


      return l;
    }
function decrypt(ciphertext, password) {
      ciphertext = String(ciphertext);
      password = String(password);
      if (ciphertext.length == 0) return ''; // nothing to decrypt

      var v = strToLongs(Buffer.from(ciphertext, 'base64').toString('binary')); //  k is 4-word key; simply convert first 16 chars of password as key
      var k = strToLongs(unescape(encodeURIComponent(password)).slice(0, 16));
      var n = v.length;
      var delta = -0x61c88647;
      var q = Math.floor(6 + 52 / n);
      var z = v[n - 1],
          y = v[0];
      var mx,
          e,
          sum = q * delta;

      while (sum != 0) {
        e = sum >>> 2 & 3;

        for (var p = n - 1; p >= 0; p--) {
          z = v[p > 0 ? p - 1 : n - 1];
          mx = (z >>> 5 ^ y << 2) + (y >>> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z);
          y = v[p] -= mx;
        }

        sum -= delta;
      }
      var str = '';
      for (var i = 0; i < v.length; i++) {
        str += String.fromCharCode(v[i] & 0xff, v[i] >>> 8 & 0xff, v[i] >>> 16 & 0xff, v[i] >>> 24 & 0xff);
      }
      return decodeURIComponent(escape(str.replace(/\0+$/, '')));
    }
