import { toast } from "sonner"

const useCustomToast = () => {
  const showSuccessToast = (description: string) => {
    toast.success("Exito", {
      description,
    })
  }

  const showErrorToast = (description: string) => {
    toast.error("Error", {
      description,
    })
  }

  return { showSuccessToast, showErrorToast }
}

export default useCustomToast
