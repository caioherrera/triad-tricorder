import { Component, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { CommonModule } from '@angular/common'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Session, SessionService } from '../../../services/session-service';

@Component({
  selector: 'session-list',
  imports: [CommonModule, MatTableModule, MatIconModule, RouterLink, RouterLinkActive, MatCheckboxModule, MatPaginatorModule, MatSortModule, MatFormFieldModule, MatInputModule ],
  templateUrl: './session-list.html',
  styleUrls: ['../../../styles.scss','./session-list.scss']
})
export class SessionListComponent { 

  sessions!: Session[];
  dataSource: MatTableDataSource<Session> = new MatTableDataSource<Session>();

  @ViewChild(MatPaginator, {static: true}) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  columnLabels: string[] = ["id", "application", "artifact", "session_type", "reference_session", "actions"];

  constructor(private sessionService: SessionService) { }

  ngOnInit(): void {
    this.sessionService.getSessions().subscribe(sessions => {
      this.sessions = sessions;
      this.dataSource.data = this.sessions; 
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort
    });
  }

  applyFilter(event: any) {
    this.dataSource.filter = event.target.value.trim().toLowerCase();
  }
}
