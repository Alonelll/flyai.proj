import { Routes } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';

export const routes: Routes = [
  { path: '', component: NavbarComponent }, // Default route
  // { path: 'about', component: AboutComponent },
  // { path: 'contact', component: ContactComponent },
  { path: '**', redirectTo: '' }, // Wildcard route for unmatched paths];
];
