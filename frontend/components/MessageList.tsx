'use client'

import { Message } from '@/types/message'
import styles from './MessageList.module.css'

interface MessageListProps {
  messages: Message[]
}

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className={styles.empty}>
        No messages yet. Be the first to send a message!
      </div>
    )
  }

  return (
    <div className={styles.messagesContainer}>
      <div className={styles.messages}>
        {messages.map((message) => (
          <div key={message.id} className={styles.message}>
            <div className={styles.messageHeader}>
              <span className={styles.username}>{message.username}</span>
              <span className={styles.timestamp}>
                {new Date(message.created_at).toLocaleTimeString()}
              </span>
            </div>
            <div className={styles.content}>{message.content}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

