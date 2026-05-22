package com.bogatti.ir.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "chat_history")
data class ChatEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val text: String,
    val sender: String,
    val timestamp: Long = System.currentTimeMillis()
)

@Dao
interface ChatDao {
    @Query("SELECT * FROM chat_history ORDER BY timestamp ASC")
    fun getAllChats(): Flow<List<ChatEntity>>

    @Insert
    suspend fun insertChat(chat: ChatEntity)

    @Query("DELETE FROM chat_history")
    suspend fun clearHistory()
}

@Database(entities = [ChatEntity::class], version = 1)
abstract class bogattiDatabase : RoomDatabase() {
    abstract fun chatDao(): ChatDao
}
