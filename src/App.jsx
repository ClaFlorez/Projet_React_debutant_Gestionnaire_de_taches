import { useEffect, useState } from 'react'

/**
 * @typedef {Object} Task
 * @property {number} id
 * @property {string} title
 * @property {boolean} done
 */

function TaskHeader() {
  return <h1>Gestionnaire de tâches</h1>
}

/** @param {{ task: Task, onToggle: (taskId: number) => void, onDelete: (taskId: number) => void }} props */
function TaskItem({ task, onToggle, onDelete }) {
  return (
    <li>
      <span
        style={{ textDecoration: task.done ? 'line-through' : 'none' }}
      >
        {task.title}
      </span>{' '}
      <button type="button" onClick={() => onToggle(task.id)}>
        Changer le statut
      </button>{' '}
      <button type="button" onClick={() => onDelete(task.id)}>
        Supprimer
      </button>
    </li>
  )
}
/** @param {{ onAdd: (title: string) => void }} props */
function TaskForm({ onAdd }) {
  const [title, setTitle] = useState('')

  /** @param {import('react').FormEvent<HTMLFormElement>} event */
  function handleSubmit(event) {
    event.preventDefault()
    const trimmedTitle = title.trim()
    if (!trimmedTitle) return

    onAdd(trimmedTitle)
    setTitle('')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
      />
      <button type="submit">Ajouter</button>
    </form>
  )
}

const API_URL = 'http://127.0.0.1:8000/tasks'

function App() {
  /** @type {[Task[], import('react').Dispatch<import('react').SetStateAction<Task[]>>]} */
  const [tasks, setTasks] = useState([])
  const [remainingOnly, setRemainingOnly] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadTasks() {
      try {
        const response = await fetch(API_URL)
        if (!response.ok) {
          throw new Error(`Erreur HTTP ${response.status}`)
        }
        const data = await response.json()
        if (!cancelled) setTasks(data)
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error ? err.message : 'Erreur de chargement',
          )
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadTasks()
    return () => {
      cancelled = true
    }
  }, [])

  /**
   * @param {string} url
   * @param {RequestInit} [options]
   */
  async function request(url, options) {
    setActionError('')
    try {
      const response = await fetch(url, options)
      if (!response.ok) {
        throw new Error(`Erreur HTTP ${response.status}`)
      }
      return await response.json()
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Erreur réseau')
      return null
    }
  }

  /** @param {string} title */
  async function addTask(title) {
    const created = await request(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })
    if (created) setTasks((currentTasks) => [...currentTasks, created])
  }

  /** @param {number} taskId */
  async function toggleTask(taskId) {
    const task = tasks.find((t) => t.id === taskId)
    if (!task) return
    const updated = await request(`${API_URL}/${taskId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !task.done }),
    })
    if (updated) {
      setTasks((currentTasks) =>
        currentTasks.map((t) => (t.id === taskId ? updated : t)),
      )
    }
  }

  /** @param {number} taskId */
  async function deleteTask(taskId) {
    const result = await request(`${API_URL}/${taskId}`, { method: 'DELETE' })
    if (result) {
      setTasks((currentTasks) => currentTasks.filter((t) => t.id !== taskId))
    }
  }
  const visibleTasks = remainingOnly
    ? tasks.filter((task) => !task.done)
    : tasks

  const remainingCount = tasks.filter((task) => !task.done).length

  useEffect(() => {
    document.title = `${remainingCount} tâche(s) restante(s)`
  }, [remainingCount])

  return (
    <main>
      <TaskHeader />
      <TaskForm onAdd={addTask} />
      <label>
        <input
          type="checkbox"
          checked={remainingOnly}
          onChange={(event) => setRemainingOnly(event.target.checked)}
        />
        Tâches restantes seulement
      </label>
      {actionError && <p role="alert">Erreur : {actionError}</p>}
      {loading ? (
        <p>Chargement...</p>
      ) : error ? (
        <p role="alert">Erreur : {error}</p>
      ) : visibleTasks.length === 0 ? (
        <p>Aucune tâche</p>
      ) : (
        <ul>
          {visibleTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={toggleTask}
              onDelete={deleteTask}
            />
          ))}
        </ul>
      )}
    </main>
  )
}

export default App

