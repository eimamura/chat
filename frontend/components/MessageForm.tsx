'use client'

import { useState, useRef, useEffect } from 'react'
import styles from './MessageForm.module.css'

interface MessageFormProps {
  onSend: (content: string) => void
  disabled?: boolean
}

export function MessageForm({ onSend, disabled }: MessageFormProps) {
  const [content, setContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [content])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim() || disabled) {
      return
    }

    const messageContent = content.trim()
    setContent('')
    setIsSubmitting(true)
    
    try {
      await onSend(messageContent)
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    } catch (err) {
      console.error('Error sending message:', err)
      // Restore content on error
      setContent(messageContent)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as any)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputGroup}>
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={disabled ? "Enter your username first..." : "Type your message... (Press Enter to send, Shift+Enter for new line)"}
          className={styles.input}
          disabled={disabled || isSubmitting}
          maxLength={1000}
          rows={1}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={!content.trim() || disabled || isSubmitting}
          title="Send message (Enter)"
        >
          {isSubmitting ? (
            <span className={styles.spinner}>⏳</span>
          ) : (
            <span>Send</span>
          )}
        </button>
      </div>
      <div className={styles.charCount}>
        {content.length}/1000
      </div>
    </form>
  )
}
