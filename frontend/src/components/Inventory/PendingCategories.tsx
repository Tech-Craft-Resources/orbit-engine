import { Skeleton } from "@/components/ui/skeleton"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const PendingCategories = () => (
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>Name</TableHead>
        <TableHead>Description</TableHead>
        <TableHead>Status</TableHead>
        <TableHead>Created</TableHead>
        <TableHead>
          <span className="sr-only">Actions</span>
        </TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      {Array.from({ length: 5 }).map((_, index) => (
        <TableRow key={index}>
          <TableCell>
            <Skeleton className="h-4 w-28" />
          </TableCell>
          <TableCell>
            <Skeleton className="h-4 w-40" />
          </TableCell>
          <TableCell>
            <div className="flex items-center gap-2">
              <Skeleton className="size-2 rounded-full" />
              <Skeleton className="h-4 w-12" />
            </div>
          </TableCell>
          <TableCell>
            <Skeleton className="h-4 w-20" />
          </TableCell>
          <TableCell>
            <div className="flex justify-end">
              <Skeleton className="size-8 rounded-md" />
            </div>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
)

export default PendingCategories
