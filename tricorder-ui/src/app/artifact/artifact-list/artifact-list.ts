import { Component, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { CommonModule } from '@angular/common'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Artifact, ArtifactService } from '../../../services/artifact-service';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'artifact-list',
  imports: [CommonModule, MatTableModule, MatIconModule, RouterLink, RouterLinkActive, MatCheckboxModule, MatPaginatorModule, MatSortModule, MatFormFieldModule, MatInputModule ],
  templateUrl: './artifact-list.html',
  styleUrls: ['../../../styles.scss','./artifact-list.scss']
})
export class ArtifactListComponent { 

  artifacts!: Artifact[];
  dataSource: MatTableDataSource<Artifact> = new MatTableDataSource<Artifact>();

  @ViewChild(MatPaginator, {static: true}) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  columnLabels: string[] = ["id", "artifact_name", "application", "file_path", "is_reference", "actions"];

  constructor(private artifactService: ArtifactService) { }

  ngOnInit(): void {
    this.artifactService.getArtifacts().subscribe(artifacts => {
      this.artifacts = artifacts;
      this.dataSource.data = this.artifacts; 
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort
    });
  }

  applyFilter(event: any) {
    this.dataSource.filter = event.target.value.trim().toLowerCase();
  }
}
