'use client'

import { useState, useEffect } from 'react'
import { Item } from '@/types/item'
import { ItemList } from '@/components/ItemList'
import { CreateItemForm } from '@/components/CreateItemForm'
import styles from './page.module.css'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchItems = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_URL}/api/items`)
      if (!response.ok) {
        throw new Error('Failed to fetch items')
      }
      const data = await response.json()
      setItems(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      console.error('Error fetching items:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchItems()
  }, [])

  const handleCreate = async (name: string) => {
    try {
      const response = await fetch(`${API_URL}/api/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
      })
      if (!response.ok) {
        throw new Error('Failed to create item')
      }
      await fetchItems()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create item')
      console.error('Error creating item:', err)
    }
  }

  const handleDelete = async (id: string) => {
    try {
      const response = await fetch(`${API_URL}/api/items/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error('Failed to delete item')
      }
      await fetchItems()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete item')
      console.error('Error deleting item:', err)
    }
  }

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>MVP Web App</h1>
      <p className={styles.description}>
        A minimal MVP demonstrating end-to-end flow: UI → API → DB → UI
      </p>

      {error && (
        <div className={styles.error}>
          Error: {error}
        </div>
      )}

      <CreateItemForm onCreate={handleCreate} />

      {loading ? (
        <div className={styles.loading}>Loading items...</div>
      ) : (
        <ItemList items={items} onDelete={handleDelete} />
      )}
    </main>
  )
}

