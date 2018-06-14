import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppMaterialModule } from './material/material.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { LayoutComponent } from './components/layout/layout.component';
import { RoutingModule } from './routing/routing.module';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AuthService } from './services/auth.service';
import { AuthGuard } from './services/auth.guard';
import { LoginComponent } from './components/login/login.component';
import { AuthInterceptor } from './services/auth.interceptor';
import { UserService } from './services/user.service';
import { ParcoursFormComponent } from './components/parcours-form/parcours-form.component';
import { CourseSelectionDialogComponent } from './components/parcours-form/course-selection-dialog.component';
import { CourseSelectionInputComponent } from './components/parcours-form/course-selection-input.component';
import { CourseService } from 'app/services/course.service';
import { MasterService } from 'app/services/master.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LayoutComponent,
    ParcoursFormComponent,
    CourseSelectionDialogComponent,
    CourseSelectionInputComponent,
    LoginComponent,
  ],
  entryComponents: [
    CourseSelectionDialogComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    AppMaterialModule,
    FlexLayoutModule,
    RoutingModule,
    HttpClientModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    AuthService,
    AuthGuard,
    CourseService,
    MasterService,
    UserService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
