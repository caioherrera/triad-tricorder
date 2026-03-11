import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { SidebarService } from '../../../services/sidebar-service';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'menu-navbar',
  imports: [MatToolbarModule, MatIconModule],
  templateUrl: './menu-navbar.html',
  styleUrl: './menu-navbar.scss'
})
export class MenuNavbarComponent { 

  constructor(private sidebarService: SidebarService) { }

  toggleSidebar() {
    this.sidebarService.toggleSidebar();
  }

}
