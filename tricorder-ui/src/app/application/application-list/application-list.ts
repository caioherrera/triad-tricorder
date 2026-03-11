import { Component, ViewChild } from '@angular/core';
import { Application, ApplicationService } from '../../../services/application-service';
import { MatIconModule } from '@angular/material/icon';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { CommonModule } from '@angular/common'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'application-list',
  imports: [CommonModule, MatTableModule, MatIconModule, RouterLink, RouterLinkActive, MatPaginatorModule, MatSortModule, MatFormFieldModule, MatInputModule ],
  templateUrl: './application-list.html',
  styleUrls: ['../../../styles.scss','./application-list.scss']
})
export class ApplicationListComponent { 

  applications!: Application[];
  dataSource: MatTableDataSource<Application> = new MatTableDataSource<Application>();

  @ViewChild(MatPaginator, {static: true}) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  columnLabels: string[] = ["id", "application_name", "command_line", "actions"];

  constructor(private applicationService: ApplicationService) { }

  ngOnInit(): void {
    this.applicationService.getApplications().subscribe(apps => {
      this.applications = apps;
      this.dataSource.data  = this.applications; 
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  applyFilter(event: any) {
    this.dataSource.filter = event.target.value.trim().toLowerCase();
  }
}
