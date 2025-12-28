'use client'

import { useEffect, useRef, useState } from 'react'
import { Message } from '@/types/message'
import styles from './MessageList.module.css'

interface MessageListProps {
  messages: Message[]
  currentUsername?: string
  containerRef?: React.RefObject<HTMLDivElement>
}

export function MessageList({ messages, currentUsername, containerRef }: MessageListProps) {
  const [visibleMessages, setVisibleMessages] = useState<Set<string>>(new Set())
  const messageRefs = useRef<Map<string, HTMLDivElement>>(new Map())

  useEffect(() => {
    // Animate new messages as they appear
    messages.forEach((msg) => {
      if (!visibleMessages.has(msg.id)) {
        setTimeout(() => {
          setVisibleMessages((prev) => new Set(prev).add(msg.id))
        }, 50)
      }
    })
  }, [messages, visibleMessages])

  if (messages.length === 0) {
    return (
      <div className={styles.empty}>
        No messages yet. Be the first to send a message!
      </div>
    )
  }

  return (
    <div className={styles.messagesContainer} ref={containerRef}>
      <div className={styles.messages}>
        {messages.map((message, index) => {
          const isOwnMessage = currentUsername && message.username === currentUsername
          const isVisible = visibleMessages.has(message.id)
          // Only animate the last message if it's newly visible
          const isNew = index === messages.length - 1 && isVisible && messages.length > 0

          return (
            <div
              key={message.id}
              ref={(el) => {
                if (el) messageRefs.current.set(message.id, el)
              }}
              className={`${styles.message} ${isOwnMessage ? styles.ownMessage : ''} ${isVisible ? styles.visible : styles.hidden}`}
            >
              <div className={styles.messageHeader}>
                <span className={styles.username}>{message.username}</span>
                <span className={styles.timestamp}>
                  {new Date(message.created_at).toLocaleTimeString()}
                </span>
              </div>
              <div className={styles.content}>
                <TypingText text={message.content} animate={isNew} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// Component for typing animation effect
function TypingText({ text, animate }: { text: string; animate: boolean }) {
  const [displayedText, setDisplayedText] = useState(text)
  const [isAnimating, setIsAnimating] = useState(false)
  const hasAnimatedRef = useRef(false)

  useEffect(() => {
    if (animate && text.length > 0 && !hasAnimatedRef.current) {
      hasAnimatedRef.current = true
      setIsAnimating(true)
      setDisplayedText('')
      let currentIndex = 0
      const interval = setInterval(() => {
        if (currentIndex < text.length) {
          setDisplayedText(text.slice(0, currentIndex + 1))
          currentIndex++
        } else {
          setIsAnimating(false)
          clearInterval(interval)
        }
      }, 15) // Adjust speed: lower = faster

      return () => clearInterval(interval)
    } else if (!animate) {
      // For non-animated messages, show immediately
      setDisplayedText(text)
      hasAnimatedRef.current = false
    }
  }, [text, animate])

  return (
    <span>
      {displayedText}
      {isAnimating && <span className={styles.cursor}>|</span>}
    </span>
  )
}
