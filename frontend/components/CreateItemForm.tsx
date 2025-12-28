'use client'

import { useState } from 'react'
import styles from './CreateItemForm.module.css'

interface CreateItemFormProps {
  onCreate: (name: string) => void
}

export function CreateItemForm({ onCreate }: CreateItemFormProps) {
  const [name, setName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) {
      return
    }

    setIsSubmitting(true)
    try {
      await onCreate(name.trim())
      setName('')
    } catch (err) {
      console.error('Error creating item:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputGroup}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter item name..."
          className={styles.input}
          disabled={isSubmitting}
          maxLength={200}
        />
        <button
          type="submit"
          className={styles.submitButton}
          disabled={!name.trim() || isSubmitting}
        >
          {isSubmitting ? 'Creating...' : 'Create Item'}
        </button>
      </div>
    </form>
  )
}

