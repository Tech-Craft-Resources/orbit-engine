import { useEffect, useRef, useState } from "react"

interface UseScrollAnimationOptions {
  /** Fraction of the element visible before triggering (0-1). Default: 0.15 */
  threshold?: number
  /** Only animate once, then stay visible. Default: true */
  once?: boolean
  /** Root margin to trigger earlier/later. Default: "0px 0px -40px 0px" */
  rootMargin?: string
}

/**
 * Returns a ref to attach to an element and a boolean indicating
 * whether the element has scrolled into view.
 */
export function useScrollAnimation<T extends HTMLElement = HTMLDivElement>(
  options: UseScrollAnimationOptions = {},
) {
  const {
    threshold = 0.15,
    once = true,
    rootMargin = "0px 0px -40px 0px",
  } = options
  const ref = useRef<T>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          if (once) {
            observer.unobserve(element)
          }
        } else if (!once) {
          setIsVisible(false)
        }
      },
      { threshold, rootMargin },
    )

    observer.observe(element)
    return () => observer.disconnect()
  }, [threshold, once, rootMargin])

  return { ref, isVisible }
}
