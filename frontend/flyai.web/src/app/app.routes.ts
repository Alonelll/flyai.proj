import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./content/content.component').then((m) => m.ContentComponent),
  },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./dashboard/dashboard.component').then((m) => m.DashboardComponent),
  },
  {
    path: 'table-results',
    loadComponent: () => import('./table/table.component').then((m) => m.TableComponent),
  },
  { path: '**', redirectTo: '' },
];
