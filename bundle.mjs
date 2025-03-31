#!/usr/bin/env node
import * as esbuild from 'esbuild'
import { argv, chdir, cwd, exit } from 'node:process'
import path from 'node:path';

const staticRoot = argv[2]

const rootDir = cwd()
const rootPackageInput = await import(`file://${rootDir}/package.json`, { with: { type: 'json' } })

const { dependencies = {}, peerDependencies = {} } = rootPackageInput['default']
const external = Object.keys({ ...dependencies, ...peerDependencies })

for (const dep of Object.keys(dependencies)) {
  const entry = import.meta.resolve(dep, `file://${rootDir}/package.json`)
  const out = `${staticRoot}/esm/${dep}.min.js`
  const packageInfo = (await import(`file://${rootDir}/node_modules/${dep}/package.json`, { with: { type: 'json' } }))['default']
  const { exports } = packageInfo
  console.info(`Bundling ${dep}`)

  let entryPoints

  if (exports === undefined || typeof exports === 'string') {
    entryPoints = [entry.slice('file://'.length)]
  } else {
    entryPoints = Object.keys(exports).map((key) => {
      const entry = import.meta.resolve(path.join(dep, key), `file://${rootDir}/package.json`)
      return entry.slice('file://'.length)
    })
  }
  await esbuild.build({
    entryPoints,
    bundle: true,
    format: 'esm',
    outdir: `${staticRoot}/esm/`,
    outbase: `${rootDir}/node_modules/`,
    banner: {
      js: `/* Django-ESM: ${packageInfo.name}@${packageInfo.version} */`,
      css: `/* Django-ESM: ${packageInfo.name}@${packageInfo.version} */`,
    },
    external,
    minify: true,
    sourcemap: true,
    platform: 'browser',
    target: 'es2020',
  })
}
