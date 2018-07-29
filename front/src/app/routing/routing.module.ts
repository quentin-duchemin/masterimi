import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { HomeComponent } from '../components/home/home.component';
import { LayoutComponent } from '../components/layout/layout.component';
import { LoginComponent } from '../components/login/login.component';
import { ParcoursIntroComponent } from '../components/parcours-intro/parcours-intro.component';
import { ParcoursCoursesFormComponent } from 'app/components/parcours-courses-form/parcours-courses-form.component';
import { AuthGuard } from '../services/auth.guard';

import { ParcoursResolver } from './parcours.resolver';
import { FormulasResolver } from './formulas.resolver';
import { MastersResolver } from './masters.resolver';
import { CoursesResolver } from './courses.resolver';


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
            component: ParcoursIntroComponent,
          },
          {
            path: '',
            resolve: {
              parcours: ParcoursResolver,
              masters: MastersResolver,
              formulas: FormulasResolver,
              courses: CoursesResolver,
            },
            children: [
              {
                path: 'show',
                component: ParcoursCoursesFormComponent,
                data: {
                  view: 'show',
                },
              },
              {
                path: 'edit',
                component: ParcoursCoursesFormComponent,
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
  imports: [
    RouterModule.forRoot(routes, {
      paramsInheritanceStrategy: 'always',
    })
  ],
  exports: [RouterModule],
  providers: [
    CoursesResolver,
    FormulasResolver,
    MastersResolver,
    ParcoursResolver,
  ],
})
export class RoutingModule {
}
