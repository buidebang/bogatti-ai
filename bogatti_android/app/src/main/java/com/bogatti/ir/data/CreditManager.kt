package com.bogatti.ir.data

import android.content.Context
import android.util.Base64
import org.json.JSONObject
import java.io.File

class CreditManager(
    private val context: Context,
    private val encryptionKey: String, // Key passed from a secure provider/config
    private val storageName: String = "credits.bin",
    private val rate: Int = 100000
) {
    private val storageFile = File(context.filesDir, storageName)
    private var balanceToman: Long = loadBalance()

    private fun xorCrypt(data: String): String {
        val result = StringBuilder()
        for (i in data.indices) {
            result.append((data[i].code xor encryptionKey[i % encryptionKey.length].code).toChar())
        }
        return result.toString()
    }

    private fun loadBalance(): Long {
        if (!storageFile.exists()) return 0
        return try {
            val encoded = storageFile.readBytes()
            val decodedB64 = String(Base64.decode(encoded, Base64.DEFAULT))
            val decrypted = xorCrypt(decodedB64)
            val json = JSONObject(decrypted)
            json.optLong("balance_toman", 0)
        } catch (e: Exception) {
            0
        }
    }

    fun saveBalance() {
        try {
            val json = JSONObject()
            json.put("balance_toman", balanceToman)
            val encrypted = xorCrypt(json.toString())
            val encoded = Base64.encode(encrypted.toByteArray(), Base64.DEFAULT)
            storageFile.writeBytes(encoded)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    val balanceUsd: Double
        get() = balanceToman.toDouble() / rate

    fun deductUsd(amountUsd: Double): Boolean {
        val amountToman = (amountUsd * rate).toLong()
        if (balanceToman >= amountToman) {
            balanceToman -= amountToman
            saveBalance()
            return true
        }
        return false
    }

    fun addToman(amountToman: Long) {
        balanceToman += amountToman
        saveBalance()
    }

    fun getBalanceUsdStr(): String {
        return String.format("%.2f", balanceUsd)
    }
}
