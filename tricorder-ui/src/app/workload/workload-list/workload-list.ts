import { Component, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { CommonModule } from '@angular/common'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Workload, WorkloadService } from '../../../services/workload-service';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'workload-list',
  imports: [CommonModule, MatTableModule, MatIconModule, RouterLink, RouterLinkActive, MatCheckboxModule, MatPaginatorModule, MatSortModule, MatFormFieldModule, MatInputModule ],
  templateUrl: './workload-list.html',
  styleUrls: ['../../../styles.scss','./workload-list.scss']
})
export class WorkloadListComponent { 

  workloads!: Workload[];
  dataSource: MatTableDataSource<Workload> = new MatTableDataSource<Workload>();

  @ViewChild(MatPaginator, {static: true}) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  columnLabels: string[] = ["id", "workload_name", "application", "workload_desc", "input_value", "actions"];

  constructor(private workloadService: WorkloadService) { }

  ngOnInit(): void {
    this.workloadService.getWorkloads().subscribe(workloads => {
      this.workloads = workloads;
      this.dataSource.data = this.workloads; 
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort
    });
  }

  applyFilter(event: any) {
    this.dataSource.filter = event.target.value.trim().toLowerCase();
  }
}
