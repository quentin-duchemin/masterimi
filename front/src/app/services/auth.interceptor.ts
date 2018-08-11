import { Injectable, Injector } from '@angular/core';
import { HttpErrorResponse, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { environment } from 'environments/environment';
import { catchError } from 'rxjs/operators';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private injector: Injector) {
  }

  private get authService(): AuthService {
    return this.injector.get(AuthService);
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<any> {
    const baseUrl = environment.baseUrl;

    // For backend API
    if (req.url.startsWith('/')) {
      req = req.clone({
        url: baseUrl + req.url,
      });

      const accessToken = this.authService.getAccessToken();
      if (accessToken) {
        req = req.clone({
          headers: req.headers.set('Authorization', `Token ${accessToken}`)
        });
      }
    }

    return next.handle(req).pipe(
      catchError((err: any) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status === 401) {
            this.authService.logout();
          }
        }

        return throwError(err);
      }),
    );
  }
}
