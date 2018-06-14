import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { HomeComponent } from 'app/components/home/home.component';
import { LayoutComponent } from 'app/components/layout/layout.component';
import { LoginComponent } from 'app/components/login/login.component';
import { ParcoursFormComponent } from 'app/components/parcours-form/parcours-form.component';
import { AuthGuard } from 'app/services/auth.guard';

import { ParcoursResolver } from './parcours.resolver';
import { CurrentUserResolver } from './current-user.resolver';
import { FormulasResolver } from './formulas.resolver';
import { DepartmentsResolver } from './departments.resolver';
import { MastersResolver } from './masters.resolver';
import { CoursesResolver } from 'app/routing/courses.resolver';


const routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [
      AuthGuard,
    ],
    resolve: {
      currentUser: CurrentUserResolver,
    },
    children: [
      {
        path: '',
        component: HomeComponent,
      },
      {
        path: 'parcours',
        children: [
          {
            path: '',
            resolve: {
              parcours: ParcoursResolver,
              departments: DepartmentsResolver,
              masters: MastersResolver,
              formulas: FormulasResolver,
              courses: CoursesResolver,
            },
            children: [
              {
                path: '',
                component: ParcoursFormComponent,
                data: {
                  view: 'show',
                },
              },
              {
                path: 'edit',
                component: ParcoursFormComponent,
                data: {
                  view: 'edit',
                },
              },
            ]
          },
        ],
      },
    ],
  },
];


@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ],
  providers: [
    CoursesResolver,
    CurrentUserResolver,
    DepartmentsResolver,
    FormulasResolver,
    MastersResolver,
    ParcoursResolver,
  ],
})
export class RoutingModule {}
