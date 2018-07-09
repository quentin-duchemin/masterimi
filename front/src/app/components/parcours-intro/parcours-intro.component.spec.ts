import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParcoursIntroComponent } from './parcours-intro.component';

describe('ParcoursIntroComponent', () => {
  let component: ParcoursIntroComponent;
  let fixture: ComponentFixture<ParcoursIntroComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParcoursIntroComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParcoursIntroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
