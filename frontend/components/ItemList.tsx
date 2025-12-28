'use client'

import { Item } from '@/types/item'
import styles from './ItemList.module.css'

interface ItemListProps {
  items: Item[]
  onDelete: (id: string) => void
}

export function ItemList({ items, onDelete }: ItemListProps) {
  if (items.length === 0) {
    return (
      <div className={styles.empty}>
        No items yet. Create one using the form above!
      </div>
    )
  }

  return (
    <div className={styles.list}>
      <h2 className={styles.listTitle}>Items ({items.length})</h2>
      <ul className={styles.items}>
        {items.map((item) => (
          <li key={item.id} className={styles.item}>
            <div className={styles.itemContent}>
              <span className={styles.itemName}>{item.name}</span>
              <span className={styles.itemDate}>
                {new Date(item.created_at).toLocaleString()}
              </span>
            </div>
            <button
              className={styles.deleteButton}
              onClick={() => onDelete(item.id)}
              aria-label={`Delete ${item.name}`}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

