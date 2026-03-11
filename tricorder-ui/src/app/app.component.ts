import { Component } from '@angular/core';
import { MenuSidebarComponent } from './menu/menu-sidebar/menu-sidebar';
import { MenuNavbarComponent } from './menu/menu-navbar/menu-navbar';
import { RouterOutlet } from '@angular/router';
import { MenuBreadCrumbComponent } from './menu/menu-breadcrumb/menu-breadcrumb';
import { SidebarService } from '../services/sidebar-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [MenuSidebarComponent, MenuNavbarComponent, MenuBreadCrumbComponent, RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {

  constructor(private sidebarService: SidebarService) { }

  isSidebarOpen: boolean = false;

  ngOnInit() {
    this.sidebarService.onSidebarToggle().subscribe((opening) => { this.isSidebarOpen = opening; });
  }

  title = 'tricorder-ui';
}
