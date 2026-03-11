import { Component } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { SidebarService } from '../../../services/sidebar-service';

@Component({
  selector: 'menu-sidebar',
  imports: [MatSidenavModule, MatIconModule, MatDividerModule, MatButtonModule, RouterLink, RouterLinkActive],
  templateUrl: './menu-sidebar.html',
  styleUrls: ['../../../styles.scss', './menu-sidebar.scss']
})
export class MenuSidebarComponent { 

  constructor(private sidebarService: SidebarService) { }

  shouldOpenSidebar: boolean = false;

  ngOnInit() {
    this.sidebarService.onSidebarToggle().subscribe((opening) => { this.shouldOpenSidebar = opening; });
  }
}
