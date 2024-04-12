import React from 'react';
import {
 ColumnDef,
 flexRender,
 getCoreRowModel,
 useReactTable,
} from "@tanstack/react-table";

import {
 Table,
 TableBody,
 TableCell,
 TableHead,
 TableHeader,
 TableRow,
} from "@/components/ui/table";

interface DataTableProps<TData, TValue> {
 columns: ColumnDef<TData, TValue>[]
 data: TData[]
}

export function DataTable<TData, TValue>({
 columns,
 data,
}: DataTableProps<TData, TValue>) {
 const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
 });

 // Function to check if a column is the "Image" column
 const isImageColumn = (column:any) => column.columnDef.header === 'Image';

 return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead key={header.id}>
                 {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                 <TableCell key={cell.id}>
                    {isImageColumn(cell.column) ? (
                   <div className='rounded border-r-5'>
                   <img src={`${cell.getValue()}`} alt="Image" className='rounded-lg border-2 w-10 h-10' />
               </div>
               
                    ) : (
                      flexRender(cell.column.columnDef.cell, cell.getContext())
                    )}
                 </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
 );
}
