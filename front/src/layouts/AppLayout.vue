<template>
  <div>

    <Head :title="title" />

    <Banner />

    <nav class="navbar navbar-expand-md navbar-light bg-white border-bottom sticky-top">
      <div class="container-fluid">
        <!-- Logo -->
        <Link class="navbar-brand me-4" :href="route('dashboard')">
        <ApplicationMark width="36" />
        </Link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Left Side Of Navbar -->
          <ul class="navbar-nav me-auto">
            <NavLink :href="route('dashboard')" :active="route().current('dashboard')">
              {{ $t('nav.home') }}
            </NavLink>
            <NavDropdown :active="route().current('admin.*')">
              <template #trigger>
                {{ $t('nav.admin') }}
              </template>
              <template #content>
                <DropdownLink :href="route('admin.filemanager')">
                  Gerenciador de arquivos
                </DropdownLink>
                <DropdownLink :href="route('admin.users.index')">
                  Usuários
                </DropdownLink>
                <DropdownLink :href="route('admin.groups.index')">
                  Grupos
                </DropdownLink>
              </template>
            </NavDropdown>
            <!-- <NavDropdown :active="route().current('itegam.*')">
                  <template #trigger>
                    ITEGAM
                  </template>
                  <template #content>
                  <DropdownLink :href="route('itegam.colaborador.index')">
                    Colaboradores
                  </DropdownLink>
                  <DropdownLink :href="route('itegam.convenio.index')">
                    Convenio
                  </DropdownLink>
                  <DropdownLink :href="route('itegam.curso-especializacao.index')">
                    Curso de Especialização
                  </DropdownLink>
                  <DropdownLink :href="route('itegam.colaborador.index')">
                    Colaboradores
                  </DropdownLink>
                  </template>
                </NavDropdown> -->
          </ul>

          <!-- Right Side Of Navbar -->
          <ul class="navbar-nav align-items-baseline">
            <!-- Language -->
            <select class="form-select" v-model="lang">
              <option value="pt-BR">PT-BR</option>
              <option value="en">EN</option>
            </select>
            <!-- Team Management -->
            <Dropdown id="teamManagementDropdown" v-if="$page.props.jetstream.hasTeamFeatures">
              <template #trigger>
                {{ $page.props.user.current_team.name }}

                <svg class="me-2" width="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd" />
                </svg>
              </template>

              <template #content>
                <!-- Team Management -->
                <template v-if="$page.props.jetstream.hasTeamFeatures">
                  <h6 class="dropdown-header">
                    Manage Team
                  </h6>

                  <!-- Team Settings -->
                  <DropdownLink :href="route('teams.show', $page.props.user.current_team)">
                    Team Settings
                  </DropdownLink>

                  <DropdownLink :href="route('teams.create')" v-if="$page.props.jetstream.canCreateTeams">
                    Create New Team
                  </DropdownLink>

                  <hr class="dropdown-divider">

                  <!-- Team Switcher -->
                  <h6 class="dropdown-header">
                    Switch Teams
                  </h6>

                  <template v-for="team in $page.props.user.all_teams" :key="team.id">
                    <form @submit.prevent="switchToTeam(team)">
                      <DropdownLink as="button">
                        <div class="d-flex">
                          <svg v-if="team.id == $page.props.user.current_team_id" class="me-1 text-success" width="20"
                            fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            stroke="currentColor" viewBox="0 0 24 24">
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                          <span class="text-truncate" style="width: 12rem;">{{ team.name }}</span>
                        </div>
                      </DropdownLink>
                    </form>
                  </template>
                </template>
              </template>
            </Dropdown>

            <!-- Authentication Links -->
            <Dropdown id="settingsDropdown">
              <template #trigger>
                <img v-if="$page.props.jetstream.managesProfilePhotos" class="rounded-circle" width="32" height="32"
                  :src="$page.props.user.profile_photo_url" :alt="$page.props.user.name" />

                <span v-else>
                  {{ $page.props.user.name }}
                </span>
              </template>

              <template #content>
                <!-- Account Management -->
                <h6 class="dropdown-header small text-muted">
                  Manage Account
                </h6>

                <DropdownLink :href="route('profile.show')">
                  Profile
                </DropdownLink>

                <DropdownLink :href="route('api-tokens.index')" v-if="$page.props.jetstream.hasApiFeatures">
                  API Tokens
                </DropdownLink>

                <hr class="dropdown-divider">

                <!-- Authentication -->
                <form @submit.prevent="logout">
                  <DropdownLink as="button">
                    Log out
                  </DropdownLink>
                </form>
              </template>
            </Dropdown>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Page Heading -->
    <header class="d-flex py-3 bg-white shadow-sm border-bottom">
      <div class="container-fluid">
        <slot name="header"></slot>
      </div>
    </header>

    <!-- Page Content -->
    <main class="container-fluid my-5">
      <slot></slot>
    </main>
  </div>
</template>

<script>
import JetApplicationLogo from '@/Components/ApplicationLogo.vue'
import Banner from '@/Components/Banner.vue'
import ApplicationMark from '@/Components/ApplicationMark.vue'
import Dropdown from '@/Components/Dropdown.vue'
import DropdownLink from '@/Components/DropdownLink.vue'
import NavLink from '@/Components/NavLink.vue'
import { Head, Link } from '@inertiajs/inertia-vue3'
import NavDropdown from '../Components/NavDropdown.vue'
import { getActiveLanguage, loadLanguageAsync } from 'laravel-vue-i18n';

export default {
  props: {
    title: String,
  },

  components: {
    Head,
    JetApplicationLogo,
    Banner,
    ApplicationMark,
    Dropdown,
    DropdownLink,
    NavLink,
    Link,
    NavDropdown
  },

  data() {
    return {
      language: getActiveLanguage(),
      showingNavigationDropdown: false,
    }
  },

  methods: {
    switchToTeam(team) {
      this.$inertia.put(route('current-team.update'), {
        'team_id': team.id
      }, {
        preserveState: false
      })
    },

    logout() {
      this.$inertia.post(route('logout'));
    },
  },

  computed: {
    path() {
      return window.location.pathname
    },
    lang: {
      get() {
        return this.language;
      },
      async set(value) {
        this.language = await loadLanguageAsync(value);
      }
    }
  }
}
</script>
