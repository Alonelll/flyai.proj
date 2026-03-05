import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./content/content.component').then((m) => m.ContentComponent),
  },
  {
    path: 'table-results',
    loadComponent: () => import('./table/table.component').then((m) => m.TableComponent),
  },
  { path: '**', redirectTo: '' },
];
